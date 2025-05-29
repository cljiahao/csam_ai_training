import ImageHolder from "@/components/widgets/image-holder/ImageHolder";
import MarkCanvas from "@/components/widgets/mark-canvas/MarkCanvas";
import SettingsFinderContext from "./context/SettingsFinderContext";
import useSettingsFinder from "./hook/useSettingsFinder";
import UploadForm from "./subfeatures/upload-form/UploadForm";

const SettingsFinder = ({ mode }) => {
  const {
    state: { markRef, image, error, coordinates },
    action: { setImage, setError },
  } = useSettingsFinder({ mode });

  const canvasType = mode.toLowerCase() === "batch" ? "rect" : "dot";

  return (
    <SettingsFinderContext.Provider value={{ setImage, setError }}>
      <div className="hw-full">
        <ImageHolder
          className="h-5/6"
          image={image}
          error={error}
          placeholder_text={mode}
        >
          <MarkCanvas
            ref={markRef}
            canvasType={canvasType}
            coordinates={coordinates}
          />
        </ImageHolder>
        <UploadForm className="h-1/6" mode={mode} />
      </div>
    </SettingsFinderContext.Provider>
  );
};

export default SettingsFinder;
