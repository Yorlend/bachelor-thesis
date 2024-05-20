export type Fingerprint = {
    name: string
    position: {
        x: number
        y: number
    }
}

export async function createFP(name: string, x: number, y: number) {
    const response = await fetch(`http://localhost:8000/fingerprints/`, {
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

export async function getFPs() {
    const response = await fetch(`http://localhost:8000/fingerprints/`)

    return await response.json()
}

export async function updateFP(name: string, x: number, y: number) {
    const response = await fetch(`http://localhost:8000/fingerprints/${name}`, {
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

export async function deleteFP(name: string) {
    const response = await fetch(`http://localhost:8000/fingerprints/${name}`, {
        method: 'DELETE',
    })

    return await response.json()
}
