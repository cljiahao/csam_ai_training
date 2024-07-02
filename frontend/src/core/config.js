import { env } from "../env";
const API = env.REACT_APP_API;

const initialDrop = {
  folder: { list: [], selected: "" },
  item: { list: [], selected: "" },
  model: { list: [], selected: "" },
  zip: { list: [], selected: "" },
};

const initialEntry = { random: "0", split: "20" };

const initialEvaluation = { actual: {}, predict: {} };

const initialRandom = { gallery: [], count: {} };

const initialGraph = { status: "complete", graph: [] };

const initialOutflow = { status: "complete", model: "", res: {} };

const initialParameters = {
  folder: "",
  model: "",
  epochs: "10",
  callbacks: {},
};

const initialAugRange = {
  input: {
    hsv: {
      "Low H": 0,
      "High H": 255,
      "Low S": 0,
      "High S": 255,
      "Low V": 0,
      "High V": 255,
    },
    mask: {
      Thresh: 230,
      Erode_x: 1,
      Erode_y: 1,
    },
  },
  slider: {
    hsv: {
      "Low H": 0,
      "High H": 255,
      "Low S": 0,
      "High S": 255,
      "Low V": 0,
      "High V": 255,
    },
    mask: {
      Thresh: 230,
      Erode_x: 1,
      Erode_y: 1,
    },
  },
};

const initialSetRange = {
  batch: {
    threshold: 0,
    close_x: 0,
    close_y: 0,
    erode_x: 0,
    erode_y: 0,
  },
  chip: {
    threshold: 0,
    close_x: 0,
    close_y: 0,
    erode_x: 0,
    erode_y: 0,
  },
};

const initialTable = {
  head1: {
    subhead1: 1,
    subhead2: 2,
    subhead3: 3,
  },
  head2: {
    subhead1: 1,
    subhead2: 2,
    subhead3: 3,
  },
};

const initialTrigger = {
  menu: false,
  outflow: false,
  verbose: false,
  image: null,
};

export {
  API,
  initialDrop,
  initialEntry,
  initialEvaluation,
  initialGraph,
  initialOutflow,
  initialParameters,
  initialRandom,
  initialAugRange,
  initialSetRange,
  initialTable,
  initialTrigger,
};
