let socket: WebSocket | null = null;

export const connectRealtime = () => {
  if (!socket || socket.readyState === WebSocket.CLOSED) {
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const host = window.location.host;
    socket = new WebSocket(`${protocol}://${host}/ws/ai`);
  }
  return socket;
};

export const disconnectRealtime = () => {
  if (socket) {
    socket.close();
    socket = null;
  }
};
