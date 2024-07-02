import React, { useContext, useRef } from "react";
import cv from "@techstark/opencv-js";
import Swal from "sweetalert2";
import { saveAs } from "file-saver";

import { FaSave } from "react-icons/fa";
import { FiUpload } from "react-icons/fi";
import { FaLaptopCode } from "react-icons/fa";
import { LiaChalkboardTeacherSolid } from "react-icons/lia";
import { IoMdSettings } from "react-icons/io";
import { FaHome } from "react-icons/fa";
import { AppContext } from "../../../../contexts/context";

import { getRange, saveParameters } from "../../utils/api_settings";
import UploadSave from "./components/UploadSave/UploadSave";
import NavBar from "../../../../common/containers/NavBar/NavBar";

const Header = () => {
  const { holder, setHolder, range, setRange } = useContext(AppContext);
  const img_ref = useRef(null);

  const process = async (e) => {
    e.preventDefault();

    const file = e.target.files[0];
    if (file) {
      e.preventDefault();
      img_ref.current.src = URL.createObjectURL(e.target.files[0]);
      img_ref.current.onload = async () => {
        try {
          const img = cv.imread(img_ref.current);

          // Split image, threshold for background only mask and return background as full white
          const channel = new cv.MatVector();
          cv.split(img, channel);
          let combine = new cv.Mat();
          for (let j = 0; j < channel.size() - 1; ++j) {
            const cn_thres = new cv.Mat();
            cv.threshold(channel.get(j), cn_thres, 130, 255, cv.THRESH_BINARY);
            if (j === 0) combine = cn_thres;
            cv.bitwise_and(combine, cn_thres, combine);
          }
          img.setTo(new cv.Scalar.all(255), combine);

          const gray = new cv.Mat();
          cv.cvtColor(img, gray, cv.COLOR_BGR2GRAY);

          setHolder({ ...holder, image: gray });
        } catch (e) {
          console.log(e);
        }
      };
    }
  };

  const save_parameters = async () => {
    const res = await saveParameters(holder.name, range);
    if (res.ok) {
      const blob = await res.blob();
      saveAs(blob, "settings.json");
      Swal.fire({
        title: "Saved",
        text: "Settings Saved. Downloading File now.",
        icon: "success",
        confirmButtonText: "OK",
      });
    }
  };

  const get_range = async () => {
    const res = await getRange(holder.name);
    if (res.ok) {
      const json = await res.json();
      setRange(json);
    }
  };

  const upload_info = {
    name: "Upload",
    type: "file",
    icon: <FiUpload />,
    style: { font: "text-3xl" },
    accept: ".png, .jpg, .jpeg",
    onClick: (e) => {
      e.currentTarget.value = "";
    },
    onChange: process,
  };
  const input_info = {
    name: "Item Code",
    type: "text",
    default: holder.name,
    onChange: (e) =>
      setHolder((prevHold) => ({ ...prevHold, name: e.target.value })),
    onfocusout: get_range,
  };
  const button_info = {
    name: "Save",
    icon: <FaSave />,
    style: { font: "text-3xl" },
    onClick: save_parameters,
  };
  const nav_info = {
    Main: {
      name: "Main",
      icon: <FaHome />,
      style: { menu: true, font: "text-3xl" },
      onClick: () => (window.location.href = "/"),
    },
    CDA: {
      name: "CDA",
      icon: <FaLaptopCode />,
      style: { menu: true, font: "text-3xl" },
      onClick: () => (window.location.href = "/CDA"),
    },
    CMT: {
      name: "CMT",
      icon: <LiaChalkboardTeacherSolid />,
      style: { menu: true, font: "text-3xl" },
      onClick: () => (window.location.href = "/CMT"),
    },
    Settings: {
      name: "Settings",
      icon: <IoMdSettings />,
      style: { menu: true, font: "text-3xl" },
      onClick: () => (window.location.href = "/Settings"),
    },
  };

  return (
    <header className="grid h-full w-full grid-cols-5 gap-5">
      <img className="hidden" alt="input" ref={img_ref} />
      <div className="col-span-3 rounded-xl bg-red-200 px-2 py-2">
        <UploadSave
          upload_info={upload_info}
          input_info={input_info}
          button_info={button_info}
        />
      </div>
      <div className="col-span-2 rounded-xl bg-red-200 px-2">
        <NavBar button_info={nav_info} />
      </div>
    </header>
  );
};

export default Header;
