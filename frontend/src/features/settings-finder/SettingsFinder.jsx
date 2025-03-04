import { useRef, useState } from "react";
import ImageHolder from "@/components/widgets/image-holder/ImageHolder";
import MarkCanvas from "@/components/widgets/mark-canvas/MarkCanvas";
import DotCanvas from "./components/DotCanvas";
import UploadForm from "./components/UploadForm";
import SettingsFinderContext from "./contexts/SettingsFinderContext";
import BoundingBoxCanvas from "./components/BoundingBoxCanvas";

const SettingsFinder = ({ mode }) => {
  const [image, setImage] = useState(null);
  const [error, setError] = useState("");

  const markRef = useRef(null);

  return (
    <SettingsFinderContext.Provider value={{ setError, setImage, markRef }}>
      <div className="hw-full">
        <ImageHolder
          className="h-5/6"
          image={image}
          error={error}
          placeholder_text={mode}
          mode={mode}
        >
          <MarkCanvas ref={markRef}>
            {mode.toLowerCase() === "batch" ? (
              <BoundingBoxCanvas mode={mode} />
            ) : (
              <DotCanvas mode={mode} />
            )}
          </MarkCanvas>
        </ImageHolder>
        <UploadForm className="h-1/6" mode={mode} />
      </div>
    </SettingsFinderContext.Provider>
  );
};

export default SettingsFinder;
