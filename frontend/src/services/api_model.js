import { createRequestOptions, sendRequest } from ".";

export const createAugment = async (item) => {
  const params = new URLSearchParams({ item });
  const url = `/api/deep_learning/augment_defects?${params.toString()}`;
  const options = createRequestOptions("POST");
  return await sendRequest(url, options);
};

export const startTrain = async (item) => {
  const params = new URLSearchParams({ item });
  const url = `/api/deep_learning/train_model?${params.toString()}`;
  const options = createRequestOptions("POST");
  return await sendRequest(url, options);
};

export const getEpoch = async () => {
  const url = `/api/deep_learning/current_epoch`;
  const options = createRequestOptions("GET");
  return await sendRequest(url, options);
};

export const startEvaluation = async (item, body) => {
  const params = new URLSearchParams({ item });
  const url = `/api/deep_learning/evaluate_model?${params.toString()}`;
  const options = createRequestOptions("POST", body);
  return await sendRequest(url, options);
};

export const getAllModels = async () => {
  const url = `/api/deep_learning/all_model_names`;
  const options = createRequestOptions("GET");
  return await sendRequest(url, options);
};

export const installModel = async (item, ai_model_name) => {
  const params = new URLSearchParams({ item, ai_model_name });
  const url = `/api/deep_learning/install_model?${params.toString()}`;
  const options = createRequestOptions("POST");
  return await sendRequest(url, options);
};

export const deleteModel = async (item, ai_model_file_name) => {
  const params = new URLSearchParams({ item, ai_model_file_name });
  const url = `/api/deep_learning/delete_model?${params.toString()}`;
  const options = createRequestOptions("Delete");
  return await sendRequest(url, options);
};
