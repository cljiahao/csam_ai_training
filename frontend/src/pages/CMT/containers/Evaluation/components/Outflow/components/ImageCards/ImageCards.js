import React from "react";

const ImageCards = ({ name, data }) => {
  return (
    <div className="mx-auto flex w-[95%] flex-col space-y-1">
      <div className="w-full">{name}</div>
      <div className="grid w-full grid-cols-8 gap-x-5 gap-y-3">
        {data.map((value) => (
          <div className="flex-center flex-col rounded-xl border border-slate-300 text-base font-normal">
            <img src={value.image_path} alt={value.name} />
            <p className="flex-center mx-auto w-full">
              {"Pred:  "}
              <span className="flex-center w-[20%] font-semibold">
                {value.pred}
              </span>
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ImageCards;
