
const REMOTE_URL = 'http://localhost:5000/';
const COMBINE_ENDPOINT = 'combine_post';
const IMAGE_URL = 'http://localhost:5000/images/';
const ENDING = '.png';

export interface ICombineElementsResponse {
    combined: string;
    image: string;
    new: boolean;
}

export interface IErrorResponse {
    error: string;
}

export async function combineElements(element1: string, element2: string, generateImage: boolean = false) {
    return fetch(REMOTE_URL + COMBINE_ENDPOINT, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "element1": element1,
            "element2": element2,
            "generate_image": generateImage
        })
    }).then(response => 
        response.json() as Promise<ICombineElementsResponse | IErrorResponse>
    );
}

// register function globally for debugging
(window as any).combineElements = combineElements;