import { createFileRequestOptions, sendRequest } from ".";

export const uploadImage = async (mode, item, targetCount, formData) => {
  const params = new URLSearchParams({ item, target_count: targetCount });
  const url = `/api/settings/${mode}?${params.toString()}`;
  const options = createFileRequestOptions("POST", formData);
  return await sendRequest(url, options);
};
