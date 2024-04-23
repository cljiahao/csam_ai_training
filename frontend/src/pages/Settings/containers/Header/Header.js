import React, { useContext, useRef } from "react";
import cv from "@techstark/opencv-js";

import { FaSave } from "react-icons/fa";
import { FiUpload } from "react-icons/fi";
import { FaLaptopCode } from "react-icons/fa";
import { LiaChalkboardTeacherSolid } from "react-icons/lia";
import { IoMdSettings } from "react-icons/io";
import { FaHome } from "react-icons/fa";
import { AppContext } from "../../../../contexts/context";

import Input from "../../../../common/components/Input";
import Upload from "../../../../common/components/Upload";
import Button from "../../../../common/components/Button";
import NavBar from "../../../../common/containers/NavBar/NavBar";
import { getRange, saveSettings } from "../../utils/api_settings";

const Header = () => {
  const { name, setName, trigger, setTrigger, setRange } =
    useContext(AppContext);
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
            cv.threshold(channel.get(j), cn_thres, 100, 255, cv.THRESH_BINARY);
            if (j === 0) combine = cn_thres;
            cv.bitwise_and(combine, cn_thres, combine);
          }
          img.setTo(new cv.Scalar.all(255), combine);

          const gray = new cv.Mat();
          cv.cvtColor(img, gray, cv.COLOR_BGR2GRAY);

          setTrigger({ ...trigger, image: gray });
        } catch (e) {
          console.log(e);
        }
      };
    }
  };

  const get_range = async () => {
    const res = await getRange(name);
    if (res.ok) {
      setRange(res.json());
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
    default: name,
    onChange: (e) => setName(e.target.value),
    onfocusout: get_range,
  };
  const button_info = {
    name: "Save",
    icon: <FaSave />,
    style: { font: "text-3xl" },
    onClick: "",
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
    <header className="flex-center h-20 w-full gap-3 2xl:h-28">
      <div className="flex-center h-full w-full rounded-xl bg-red-200 px-2">
        <img className="hidden" alt="input" ref={img_ref} />
        <div className="w-48">
          <Upload name="upload" upload_info={upload_info} />
        </div>
        <div className="h-[75%] w-full text-base 2xl:text-lg">
          <Input name="item" input_info={input_info} />
        </div>
        <div className="w-44">
          <Button name="save" button_info={button_info} />
        </div>
      </div>
      <div className="h-full w-[60%] rounded-xl bg-red-200">
        <NavBar button_info={nav_info} />
      </div>
    </header>
  );
};

export default Header;
