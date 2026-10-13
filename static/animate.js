gsap.to("#bessie", { x: "250%", duration: 3, ease: "power2.in" });
gsap.registerEase("wheelspin", (t) => {
  const invT = 1 - t;
  return 1.35 * (1 - Math.pow(invT, 3)) - 0.35 * (1 - Math.pow(invT, 4));
});
const wheel = {
  rotation: 1440,
  transformOrigin: "50% 50%",
  duration: 5,
  ease: "wheelspin",
};
gsap.to("#right_wheel", wheel);
gsap.to("#left_wheel", wheel);
