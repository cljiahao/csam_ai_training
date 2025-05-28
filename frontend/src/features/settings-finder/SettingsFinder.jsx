import { useRef, useState } from "react";
import ImageHolder from "@/components/widgets/image-holder/ImageHolder";
import MarkCanvas from "@/components/widgets/mark-canvas/MarkCanvas";
import UploadForm from "./components/UploadForm";
import SettingsFinderContext from "./contexts/SettingsFinderContext";
import { useQuery } from "@tanstack/react-query";

const SettingsFinder = ({ mode }) => {
  const [image, setImage] = useState(null);
  const [error, setError] = useState("");

  const { data: processImageData } = useQuery({
    queryKey: ["processedSettings", mode],
  });

  const markRef = useRef(null);
  const canvasType = mode.toLowerCase() === "batch" ? "rect" : "dot";

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
          <MarkCanvas
            ref={markRef}
            canvasType={canvasType}
            coordinates={processImageData?.coordinates}
          />
        </ImageHolder>
        <UploadForm className="h-1/6" mode={mode} />
      </div>
    </SettingsFinderContext.Provider>
  );
};

export default SettingsFinder;
