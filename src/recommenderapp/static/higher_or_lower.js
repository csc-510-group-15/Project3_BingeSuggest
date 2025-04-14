/**
Copyright (c) 2025 Adam Imbert, Krishna Pallavalli, Hanqi Chen
This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks
 */

let apiKey = "";

async function fetchApiKey() {
    try {
        const response = await fetch("/get_api_key");
        const data = await response.json();
        if (data.apikey) {
            apiKey = data.apikey; // Assign the API key
        } else {
            console.error("Failed to fetch API key:", data.error);
        }
    } catch (error) {
        console.error("Error fetching API key:", error);
    }
}

fetchApiKey();

function fetchMovieData(imdbID){
    return new Promise(function(resolve, reject){
        $.ajax({
            type: 'GET',
            url: 'http://www.omdbapi.com/',
            dataType: 'json',
            data: {
                i: imdbID,
                apikey: apiKey,
            },
            success: function(response) {
                resolve(response);
            },
            error: function(error) {
                reject(error);
            }
            });
        });
}