/**
 * @Fetcher
 */
class Fetcher {
    async createUser(name, birth, center, type, called) {
        return await fetchHelper.post(
            `/backend-api/user`,
            {
                name: name,
                birth: birth,
                center: center,
                type: type,
                called: called
            }
        )
    }

    async getUser(id) {
        return await fetchHelper.get(
            `/backend-api/user/${id}`
        )
    }

    calibrate(user_id) {
        return fetchHelper.postAndForget(
            `/backend-api/camera/calibrate`,
            {
                user_id: user_id
            }
        )
    }

    calibration_delete(user_id) {
        return fetchHelper.delete(
            `/backend-api/camera/calibrate/u/${user_id}`
        )
    }

    calibration_test(user_id) {
        return fetchHelper.postAndForget(
            `/backend-api/camera/calibrate/test/u/${user_id}`
        )
    }

    record(video_id, user_id) {
        return fetchHelper.postAndForget(
            `/backend-api/camera/record`,
            {
                video_id: video_id,
                user_id: user_id
            }
        )
    }

    stop(user_id) {
        return fetchHelper.postAndForget(
            `/backend-api/camera/stop`,
            {
                user_id: user_id
            }
        )
    }

    monitor() {
        return fetchHelper.get(
            `/backend-api/camera/monitor`
        )
    }

    async openai(text) {
        return await fetchHelper.postBlob(
            `/backend-api/openai`,
            {
                text: text
            }
        )
    }

    async getEverySolution() {
        return await fetchHelper.get(
            `/backend-api/solution`,
        )
    }

    async getSolution(id) {
        return await fetchHelper.getBlob(
            `/backend-api/solution/v/${id}`,
        )
    }

    csv(user_id, time, type, video_id) {
        return fetchHelper.postAndForget(
            `/backend-api/csv`,
            {
                user_id: user_id,
                time: time,
                type: type,
                video_id: video_id
            }
        )
    }

    txt(user_id) {
        return fetchHelper.postAndForget(
            `/backend-api/txt`,
            {
                user_id: user_id
            }
        )
    }
}

/**
 * @export
 */
export const fetcher = new Fetcher();


/**
 * @FetchHelper
 */
class FetchHelper {
    postAndForget(url, body) {
        fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        });
    }

    async post(url, body) {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(body)
        });
        const json_response = await response.json();
        
        if (json_response.error) {
            console.log(json_response)
            return json_response;
        }

        return json_response.data;
    }

    async postBlob(url, body) {
        const response = await fetch(url, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            console.log(await response.json());
            return;
        }

        const blob_response = await response.blob();
        return blob_response;
    }

    async get(url, params) {
        const response = await fetch(url, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
            params: params
        });
        const json_response = await response.json();
        
        if (json_response.error) {
            console.log(json_response)
            return;
        }

        return json_response.data
    }

    async getBlob(url) {
        try {
            const response = await fetch(url, {
                method: "GET",
            });

            if (!response.ok) {
                const errorData = await response.text();
                console.error(`Failed to fetch ${url}: ${response.status} ${response.statusText}`, errorData);
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const blob_response = await response.blob();
            
            if (blob_response.size === 0) {
                console.error(`Empty blob received from ${url}`);
                return null;
            }
            
            return blob_response;
        } catch (error) {
            console.error(`Network error fetching ${url}:`, error);
            throw error;
        }
    }

    async patch(url, body) {
        const response = await fetch(url, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(body)
        });
        const json_response = await response.json();
        
        if (json_response.error) {
            console.log(json_response)
            return;
        }

        return json_response.data;
    }

    async delete(url, body) {
        const options = {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            }
        };

        if (body) {
            options.body = JSON.stringify(body);
        }

        const response = await fetch(url, options);
        const json_response = await response.json();
        
        if (json_response.error) {
            console.log(json_response)
            return;
        }

        return json_response.data;
    }
}


/**
 * @export
 */
export const fetchHelper = new FetchHelper();