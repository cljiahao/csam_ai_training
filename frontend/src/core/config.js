const API = process.env.REACT_APP_API;

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
  hsv: {
    "Low H": 1,
    "High H": 255,
    "Low S": 1,
    "High S": 255,
    "Low V": 15,
    "High V": 255,
  },
  mask: {
    Thresh: 1,
    Erode_x: 1,
    Erode_y: 1,
  },
};

const initialSetRange = {
  input: {
    batch: {
      threshold: 1,
      close_x: 1,
      close_y: 1,
      erode_x: 1,
      erode_y: 1,
    },
    chip: {
      threshold: 1,
      close_x: 1,
      close_y: 1,
      erode_x: 1,
      erode_y: 1,
    },
  },
  slider: {
    batch: {
      threshold: 1,
      close_x: 1,
      close_y: 1,
      erode_x: 1,
      erode_y: 1,
    },
    chip: {
      threshold: 1,
      close_x: 1,
      close_y: 1,
      erode_x: 1,
      erode_y: 1,
    },
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
