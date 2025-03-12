import { createRequestOptions, sendRequest } from ".";

export const createAugment = async (item) => {
  const url = `/api/model/start_augment?item=${item}`;
  const options = createRequestOptions("POST");
  return await sendRequest(url, options);
};

export const startTrain = async (item) => {
  const url = `/api/model/start_train?item=${item}`;
  const options = createRequestOptions("POST");
  return await sendRequest(url, options);
};

export const getEpoch = async () => {
  const url = `/api/model/get_epoch`;
  const options = createRequestOptions("GET");
  return await sendRequest(url, options);
};

export const startEvaluation = async (item, body) => {
  const url = `/api/model/start_evaluate?item=${item}`;
  const options = createRequestOptions("POST", body);
  return await sendRequest(url, options);
};
