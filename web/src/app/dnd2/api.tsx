
// curl -X POST -H "Content-Type: application/json" -d '{"generate_image":true,"element1":"fire","element2":"water"}' http://localhost:5000/combine_post

export interface CombinationResult {
    combined: string;
    image: string;
    new: boolean;
}

export const IMAGE_URL = "http://localhost:5000/";
export const API_URL = "http://localhost:5000/";

export function combinePost(element1: string, element2: string, 
    generateImage = true, subtract = false) {
    // TODO: extra long timeout for image generation
    console.log("combinePost", element1, element2, generateImage, subtract);
    return fetch(`${API_URL}combine_post`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            generate_image: generateImage,
            element1: element1,
            element2: element2,
            // operator: subtract ? "-" : undefined
            operator: subtract ? "without" : undefined
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        return data as CombinationResult;
        // return {
        //     combined: data.combined,
        //     image: IMAGE_URL + data.image,
        //     new: data.new
        // } as CombinationResult;
    });
}