const API = process.env.REACT_APP_API;

const initialDrop = {
  folder: { list: [], selected: "" },
  item: { list: [], selected: "" },
  model: { list: [], selected: "" },
};

const initialEntry = { target: "10000", split: "20" };

const initialRandom = { gallery: [], count: {} };

const initialGraph = { status: "complete", graph: [] };

const initialOutflow = { status: "complete", res: {} };

const initialParameters = {
  folder: "",
  model: "",
  epochs: "10",
  callbacks: {},
};

const initialRange = { input: {}, slider: {} };

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
  initialGraph,
  initialOutflow,
  initialParameters,
  initialRandom,
  initialRange,
  initialTable,
  initialTrigger,
};
