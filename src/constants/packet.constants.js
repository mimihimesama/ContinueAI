import { stringToCamelCase, stringToPascalCase } from '../utils/transform-case.utils.js';

const packagePrefix = 'Google.Protobuf.Protocol.';

export const headerConstants = {
  // bytes
  TOTAL_LENGTH: 4,
  PACKET_TYPE_LENGTH: 1,
};

export const packetTypes = {
  C_ENTER: 0,
  S_ENTER: 1,
  S_SPAWN: 2,
  S_DESPAWN: 5,
  C_MOVE: 6,
  S_MOVE: 7,
  C_ANIMATION: 8,
  S_ANIMATION: 9,
};

export const packetNames = Object.fromEntries(
  Object.entries(packetTypes).map(([key, value]) => {
    const str = packagePrefix + key.substring(0, 2) + stringToPascalCase(key.substring(2));
    return [value, str];
  }),
);

/**
 *
 * @param {number} packetType packetTypes에 매핑된 타입
 * @returns packetType에 맞는 Message 이름 반환
 */
export const getPacketNameByPacketType = (packetType) => {
  if (Object.values(packetNames).includes(packetType)) {
    return packetNames[packetType];
  }
  return null;
};

// const payloadNames = Object.fromEntries(
//   Object.entries(packetTypes).map(([key, value]) => {
//     return [value, stringToCamelCase(key)];
//   }),
// );
