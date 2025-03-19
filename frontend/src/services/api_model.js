import { createRequestOptions, sendRequest } from ".";

export const createAugment = async (item) => {
  const params = new URLSearchParams({ item });
  const url = `/api/model/start_augment?${params.toString()}`;
  const options = createRequestOptions("POST");
  return await sendRequest(url, options);
};

export const startTrain = async (item) => {
  const params = new URLSearchParams({ item });
  const url = `/api/model/start_train?${params.toString()}`;
  const options = createRequestOptions("POST");
  return await sendRequest(url, options);
};

export const getEpoch = async () => {
  const url = `/api/model/get_epoch`;
  const options = createRequestOptions("GET");
  return await sendRequest(url, options);
};

export const startEvaluation = async (item, body) => {
  const params = new URLSearchParams({ item });
  const url = `/api/model/start_evaluate?${params.toString()}`;
  const options = createRequestOptions("POST", body);
  return await sendRequest(url, options);
};
