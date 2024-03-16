
// curl -X POST -H "Content-Type: application/json" -d '{"generate_image":true,"element1":"fire","element2":"water"}' http://localhost:5000/combine_post

export interface CombinationResult {
    combined: string;
    image: string;
    new: boolean;
}

export function combinePost(element1: string, element2: string, generateImage = false) {
    return fetch('http://localhost:5000/combine_post', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            generate_image: generateImage,
            element1: element1,
            element2: element2
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        return data as CombinationResult;
    });
}