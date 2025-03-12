import { createRequestOptions, sendRequest } from ".";

export const getImageSrc = async (src_path) => {
    const url = `/api/image/${src_path}`;
    const options = createRequestOptions("GET");
    return await sendRequest(url, options);
  };