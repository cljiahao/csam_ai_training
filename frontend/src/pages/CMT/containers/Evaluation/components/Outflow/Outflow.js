import React, { useContext } from "react";
import { RxCross2 } from "react-icons/rx";
import { AppContext } from "../../../../../../contexts/context";
import Gallery from "./components/Gallery/Gallery";

const Outflow = () => {
  const { trigger, setTrigger } = useContext(AppContext);

  const image_info = {
    Mass_Lot: {
      A_1: {
        B: [
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\B\\1 NG_11_20_2646_1906.png",
            name: "1 NG_11_20_2646_1906.png",
            label: "B",
            pred: "G",
          },
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\B\\1 NG_12_23_3142_1220.png",
            name: "1 NG_12_23_3142_1220.png",
            label: "B",
            pred: "G",
          },
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\B\\1 NG_12_25_3102_1219.png",
            name: "1 NG_12_25_3102_1219.png",
            label: "B",
            pred: "G",
          },
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\B\\1 NG_6_11_2402_349.png",
            name: "1 NG_6_11_2402_349.png",
            label: "B",
            pred: "G",
          },
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\B\\1 NG_6_17_2478_304.png",
            name: "1 NG_6_17_2478_304.png",
            label: "B",
            pred: "G",
          },
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\B\\1 NG_6_9_2481_352.png",
            name: "1 NG_6_9_2481_352.png",
            label: "B",
            pred: "G",
          },
        ],
        C: [
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\C\\1 NG_11_20_2646_1906.png",
            name: "1 NG_11_20_2646_1906.png",
            label: "C",
            pred: "G",
          },
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\C\\1 NG_12_23_3142_1220.png",
            name: "1 NG_12_23_3142_1220.png",
            label: "C",
            pred: "G",
          },
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\C\\1 NG_6_17_2478_304.png",
            name: "1 NG_6_17_2478_304.png",
            label: "C",
            pred: "G",
          },
        ],
      },
      B_1: {
        B: [
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\B\\1 NG_11_20_2646_1906.png",
            name: "1 NG_11_20_2646_1906.png",
            label: "B",
            pred: "G",
          },
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\B\\1 NG_12_23_3142_1220.png",
            name: "1 NG_12_23_3142_1220.png",
            label: "B",
            pred: "G",
          },
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\B\\1 NG_12_25_3102_1219.png",
            name: "1 NG_12_25_3102_1219.png",
            label: "B",
            pred: "G",
          },
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\B\\1 NG_6_11_2402_349.png",
            name: "1 NG_6_11_2402_349.png",
            label: "B",
            pred: "G",
          },
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\B\\1 NG_6_17_2478_304.png",
            name: "1 NG_6_17_2478_304.png",
            label: "B",
            pred: "G",
          },
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\B\\1 NG_6_9_2481_352.png",
            name: "1 NG_6_9_2481_352.png",
            label: "B",
            pred: "G",
          },
        ],
        C: [
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\C\\1 NG_11_20_2646_1906.png",
            name: "1 NG_11_20_2646_1906.png",
            label: "C",
            pred: "G",
          },
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\C\\1 NG_12_23_3142_1220.png",
            name: "1 NG_12_23_3142_1220.png",
            label: "C",
            pred: "G",
          },
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\C\\1 NG_6_17_2478_304.png",
            name: "1 NG_6_17_2478_304.png",
            label: "C",
            pred: "G",
          },
        ],
      },
      C_1: {
        B: [
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\B\\1 NG_11_20_2646_1906.png",
            name: "1 NG_11_20_2646_1906.png",
            label: "B",
            pred: "G",
          },
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\B\\1 NG_12_23_3142_1220.png",
            name: "1 NG_12_23_3142_1220.png",
            label: "B",
            pred: "G",
          },
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\B\\1 NG_12_25_3102_1219.png",
            name: "1 NG_12_25_3102_1219.png",
            label: "B",
            pred: "G",
          },
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\B\\1 NG_6_11_2402_349.png",
            name: "1 NG_6_11_2402_349.png",
            label: "B",
            pred: "G",
          },
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\B\\1 NG_6_17_2478_304.png",
            name: "1 NG_6_17_2478_304.png",
            label: "B",
            pred: "G",
          },
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\B\\1 NG_6_9_2481_352.png",
            name: "1 NG_6_9_2481_352.png",
            label: "B",
            pred: "G",
          },
        ],
        C: [
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\C\\1 NG_11_20_2646_1906.png",
            name: "1 NG_11_20_2646_1906.png",
            label: "C",
            pred: "G",
          },
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\C\\1 NG_12_23_3142_1220.png",
            name: "1 NG_12_23_3142_1220.png",
            label: "C",
            pred: "G",
          },
          {
            image_path:
              "C:\\Users\\MES21106\\Desktop\\CSAM Code\\v2\\AI Training\\backend\\evaluation\\P_Mass_Lot\\A_1\\C\\1 NG_6_17_2478_304.png",
            name: "1 NG_6_17_2478_304.png",
            label: "C",
            pred: "G",
          },
        ],
      },
    },
  };

  return (
    <div className="absolute left-1/2 top-1/2 flex h-[95%] w-[95%] -translate-x-1/2 -translate-y-1/2 transform flex-col overflow-auto rounded-3xl bg-white">
      <div className="flex-end w-full p-2">
        <button
          onClick={() =>
            setTrigger((prevTrigger) => ({
              ...prevTrigger,
              outflow: !prevTrigger.outflow,
            }))
          }
        >
          <RxCross2 size="1.5rem" />
        </button>
      </div>
      <div className="flex w-full flex-1 flex-col space-y-3 overflow-y-scroll px-5 text-lg font-semibold">
        <Gallery data={image_info} />
      </div>
    </div>
  );
};

export default Outflow;
