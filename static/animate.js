function registerAnimation() {
  const wheel = {
    rotation: 1440,
    transformOrigin: "50% 50%",
    duration: 5,
    ease: "wheelspin",
  };
  gsap.registerEase("wheelspin", (t) => {
    const invT = 1 - t;
    return 1.35 * (1 - Math.pow(invT, 3)) - 0.35 * (1 - Math.pow(invT, 4));
  });

  const van = document.getElementById("vanimation");
  const background = document.getElementById("background");

  document.getElementById("spinner").classList.add("hidden");
  background.classList.remove("hidden");
  van.classList.remove("hidden");

  const resize = () => {
    const rect = background.getBoundingClientRect();
    if (rect.width < rect.height) {
      van.setAttribute("viewBox", "0 0 2000 1000");
    } else {
      van.setAttribute("viewBox", "-1000 0 4000 1000");
    }
  };

  resize();
  const observer = new ResizeObserver(resize);
  observer.observe(background);

  return gsap
    .timeline({ delay: 1 })
    .to("#bessie", { x: "250%", duration: 3, ease: "power2.in" })
    .to("#right_wheel", wheel, "<")
    .to("#left_wheel", wheel, "<");
}

function waitForImage() {
  return new Promise((resolve, reject) => {
    const image = document.getElementById("background");
    if (!image) reject("image element not found");
    else if (image.complete) resolve("image loaded");
    else {
      document.getElementById("spinner").classList.remove("hidden");
      image.addEventListener("load", () => resolve("image loaded"));
      image.addEventListener("error", () => reject("image failed to load"));
    }
  });
}

function main() {
  waitForImage().finally(registerAnimation);
}

main();
