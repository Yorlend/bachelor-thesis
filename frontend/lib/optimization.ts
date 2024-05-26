let optimizer_promise: Promise<void> | null = null;

export async function startOptimization(iterations: number, particles: number) {
  optimizer_promise = (async () => {
    await useFetch("http://localhost:8000/optimization/start", {
      method: "POST",
      body: {
        topology: {
          vertices: [
            [0, 0],
            [0, 50],
            [50, 50],
            [50, 0],
          ],
        },
        n_iterations: iterations,
        n_particles: particles,
      },
    });
  })();
}

export async function cancelOptimization() {
  await fetch("http://localhost:8000/optimization/cancel");
}

export async function getProgress(): Promise<number> {
  const response = await fetch("http://localhost:8000/optimization/status");
  return (await response.json()).progress * 100;
}

export async function optimizationDone(): Promise<boolean> {
  const response = await fetch("http://localhost:8000/optimization/status");
  return (await response.json()).status == "done";
}
