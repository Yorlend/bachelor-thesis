export type LocalizationResponse = {
    x: number
    y: number
    distance: number
}

export async function localize(x: number, y: number): Promise<LocalizationResponse> {
    const response = await fetch('http://localhost:8000/locate/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            x: x,
            y: y,
            topology: {
                vertices: []
            }
        }),
    }) 

    return await response.json()
}