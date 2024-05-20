export type Router = {
    name: string
    position: {
        x: number
        y: number
    }
}

export async function addRouter(name: string, x: number, y: number) {
    const response = await fetch(`http://localhost:8000/routers/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: name,
            position: [x, y],
        }),
    })

    return await response.json()
}

export async function getRouters(): Promise<Router[]> {
    const response = await fetch(`http://localhost:8000/routers/`)

    return await response.json()
}

export async function updateRouter(name: string, x: number, y: number) {
    const response = await fetch(`http://localhost:8000/routers/${name}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            position: [x, y],
        }),
    })

    return await response.json()
}

export async function deleteRouter(name: string) {
    const response = await fetch(`http://localhost:8000/routers/${name}`, {
        method: 'DELETE',
    })

    return await response.json()
}
