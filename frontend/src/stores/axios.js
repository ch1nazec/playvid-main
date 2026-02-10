import axios from "axios";

const api = axios.create();
const authAPI = axios.create();

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        if (error.response.status === 401) {
            const { data } = await authAPI.post('/api/refresh');
            localStorage.setItem('accessToken', data.accessToken);

            originalRequest.headers.Authorization = `Bearer ${data.accessToken}`;
            return api(error.config)
        }
        return Promise.reject(error);
    }
)