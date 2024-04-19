import { API } from "../../../core/config";

export const getFolderName = async (item) => {
  const resp = await fetch(`${API}/CMT/ds_folders`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ item: item }),
  });
  const json = await resp.json();
  return json;
};

export const getEvalFolder = async (item) => {
  const resp = await fetch(`${API}/CMT/eval_folders`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ item: item }),
  });
  const json = await resp.json();
  return json;
};

export const getAllModels = async () => {
  const resp = await fetch(`${API}/CMT/all_models`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  });
  const json = await resp.json();
  return json;
};

export const getFileCount = async (item, folder) => {
  const resp = await fetch(`${API}/CMT/ds_file_count`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ item: item, folder: folder }),
  });
  const json = await resp.json();
  return json;
};

export const zipModel = async (model_path) => {
  const resp = await fetch(`${API}/CMT/zip_model`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ m_path: model_path }),
  });
  return resp;
};
