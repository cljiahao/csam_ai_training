import React from "react";
import ImageCards from "../ImageCards/ImageCards";
import ImageExpand from "../ImageExpand.js/ImageExpand";

const Gallery = ({ data }) => {
  return (
    <div className="flex w-full flex-col space-y-2">
      {Object.keys(data).map((key) =>
        key === "res" ? (
          <ImageCards key={key} name={key} data={data[key]["outflow"]} />
        ) : (
          <ImageExpand key={key} name={key} data={data[key]} />
        ),
      )}
    </div>
  );
};

export default Gallery;
