import { API_URL } from "@/core/config";
import { createRequestOptions, sendRequest } from ".";

export const getExample = async () => {
  return await sendRequest(`${API_URL}/example`);
};

export const setExample = async (example, example_data) => {
  const options = createRequestOptions("POST", example_data);
  return await sendRequest(`${API_URL}/colors/${example}`, options);
};
