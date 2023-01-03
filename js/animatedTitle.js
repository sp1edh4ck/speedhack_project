const frames = ['speedhack'];

setInterval(
  () => {
    const frame = frames.shift();
    document.title = frame;
    frames.push(frame);
  },
  550,
);