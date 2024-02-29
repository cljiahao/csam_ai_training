import React from "react";

import Card from "./components/Card/Card";
import ExpandCard from "./components/ExpandCard/ExpandCard";

const List = ({ data, preds }) => {
  return (
    <>
      {Object.keys(data).map((key) =>
        data[key].constructor !== Object ? (
          <Card key={key} name={key} value={data[key]} pred={preds[key]} />
        ) : (
          <ExpandCard
            key={key}
            name={key}
            values={data[key]}
            preds={preds[key]}
          />
        ),
      )}
    </>
  );
};

export default List;
