const API = process.env.REACT_APP_API;

const initialDrop = {
  folder: [],
  item: [],
};

const initialEntry = { target: 10000, split: 20 };

const initialFileCount = { ng: null, others: null, g: null };

const initialGraph = { status: "complete", graph: [] };

const initialParameters = { folder: "---", epochs: 10 };

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
  initialFileCount,
  initialGraph,
  initialParameters,
  initialRange,
  initialTable,
  initialTrigger,
};
