const net = require('net');
const path = require('path');
const protobuf = require('protobufjs');

const clients = new Set();              // 연결된 클라이언트
const playerStates = new Map();         // 플레이어 ID별 상태 정보
const generatedChunks = new Map();      // 청크 캐시

let PlayerState = null;
let MapChunkRequest = null;
let MapChunkData = null;
let MapTile = null;

// === .proto 파일 로딩
const statePath = path.join(__dirname, './protobuf/PlayerState.proto');
const mapChunkPath = path.join(__dirname, './protobuf/MapChunk.proto');

protobuf.load([statePath, mapChunkPath], (err, root) => {
  if (err) throw err;

  PlayerState = root.lookupType('PlayerState');
  MapChunkRequest = root.lookupType('MapChunkRequest');
  MapChunkData = root.lookupType('MapChunkData');
  MapTile = root.lookupType('MapTile');

  console.log('[서버 준비 완료] Protobuf 로딩 완료.');
});

// === TCP 서버 시작
const server = net.createServer((socket) => {
  console.log('클라이언트 접속됨');
  clients.add(socket);

  let buffer = Buffer.alloc(0); // 수신용 버퍼

  socket.on('data', (data) => {
    buffer = Buffer.concat([buffer, data]);

    while (buffer.length >= 5) {
      const totalLength = buffer.readUInt32LE(0);
      if (buffer.length < totalLength) break;

      const packetType = buffer.readUInt8(4);
      const body = buffer.slice(5, totalLength);

      handlePacket(packetType, body, socket);
      buffer = buffer.slice(totalLength);
    }
  });

  socket.on('close', () => {
    console.log('클라이언트 연결 종료');
    clients.delete(socket);
  });

  socket.on('error', (err) => {
    console.error('[소켓 오류]', err.message);
    clients.delete(socket);
  });
});

server.listen(3000, () => {
  console.log('[서버 실행 중] 포트 3000');
});

function handlePacket(type, body, socket) {
  if (type === 1) {
    // === 플레이어 상태 수신
    const update = PlayerState.decode(body);

    const now = new Date().toLocaleString('ko-KR', { hour12: false, timeZone: 'Asia/Seoul' });
    console.log(`[${now}] PlayerState 수신: ${update.playerId} ` +
                `pos=(${update.posX.toFixed(2)}, ${update.posY.toFixed(2)}, ${update.posZ.toFixed(2)}) ` +
                `hp=${update.hp} atk=${update.atk} atkSpeed=${update.atkSpeed} moveSpeed=${update.moveSpeed} exp=${update.exp} ` +
                `running=${update.isRunning} attacking=${update.isAttacking}`);

    // === 플레이어 상태 저장 (필드 전부)
    playerStates.set(update.playerId, {
      posX: update.posX,
      posY: update.posY,
      posZ: update.posZ,
      hp: update.hp,
      atk: update.atk,
      atkSpeed: update.atkSpeed,
      moveSpeed: update.moveSpeed,
      exp: update.exp,
      isRunning: update.isRunning,
      isAttacking: update.isAttacking
    });

    // === 브로드캐스트 (타입 11)
    const encoded = PlayerState.encode(update).finish();
    const header = Buffer.alloc(4);
    header.writeUInt32LE(encoded.length + 5, 0);

    const packet = Buffer.concat([
      header,
      Buffer.from([11]),
      encoded
    ]);

    broadcastToOthers(socket, packet);
  }

  else if (type === 20) {
    // === 청크 요청 처리
    const req = MapChunkRequest.decode(body);
    console.log(`[청크 요청] ${req.playerId} → (${req.chunkX}, ${req.chunkZ})`);

    const chunkKey = `${req.chunkX}_${req.chunkZ}`;
    let chunkData = generatedChunks.get(chunkKey);

    if (!chunkData) {
      console.log(`[캐싱] 새 청크 생성: ${chunkKey}`);
      chunkData = createChunkData(req.chunkX, req.chunkZ);
      generatedChunks.set(chunkKey, chunkData);
    } else {
      console.log(`[캐싱] 기존 청크 제공: ${chunkKey}`);
    }

    const encoded = MapChunkData.encode(chunkData).finish();
    const header = Buffer.alloc(4);
    header.writeUInt32LE(encoded.length + 5, 0);

    const packet = Buffer.concat([
      header,
      Buffer.from([21]),
      encoded
    ]);

    socket.write(packet);
  }

  else {
    console.log('[경고] 알 수 없는 패킷 타입:', type);
  }
}

// === 청크 생성 함수 (기본 3x3 타일)
function createChunkData(cx, cz) {
  const tileWorldSize = 30;
  const tiles = [];

  for (let tx = -1; tx <= 1; tx++) {
    for (let tz = -1; tz <= 1; tz++) {
      const tileType = Math.random() < 0.1 ? 1 : 0;
      const posX = cx * 3 * tileWorldSize + tx * tileWorldSize;
      const posZ = cz * 3 * tileWorldSize + tz * tileWorldSize;

      tiles.push(MapTile.create({
        tileType,
        posX,
        posZ,
        tileX: tx,
        tileZ: tz
      }));
    }
  }

  return MapChunkData.create({
    chunkX: cx,
    chunkZ: cz,
    tiles
  });
}

// === 클라이언트 전체에 브로드캐스트 (보낸 사람 제외)
function broadcastToOthers(sender, packet) {
  for (const client of clients) {
    if (client !== sender) {
      client.write(packet);
    }
  }
}
