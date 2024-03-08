import React from "react";

import Card from "./components/Card/Card";
import ExpandCard from "./components/ExpandCard/ExpandCard";

const List = ({ actual, predict }) => {
  return (
    <>
      {Object.keys(actual).map((key) =>
        Object.keys(actual[key]).includes("res") ? (
          <Card
            key={key}
            name={key}
            value={actual[key].res.counter}
            pred={predict[key].res.counter}
          />
        ) : (
          <ExpandCard
            key={key}
            name={key}
            values={actual[key]}
            preds={predict[key]}
          />
        ),
      )}
    </>
  );
};

export default List;
