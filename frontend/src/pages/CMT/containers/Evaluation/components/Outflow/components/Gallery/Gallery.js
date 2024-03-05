import React from "react";
import ImageCards from "../ImageCards/ImageCards";
import ImageExpand from "../ImageExpand.js/ImageExpand";

const Gallery = ({ data }) => {
  return (
    <div className="flex w-full flex-col space-y-2">
      {Object.keys(data).map((key) =>
        data[key].constructor !== Object ? (
          <ImageCards key={key} name={key} data={data[key]} />
        ) : (
          <ImageExpand key={key} name={key} data={data[key]} />
        ),
      )}
    </div>
  );
};

export default Gallery;
