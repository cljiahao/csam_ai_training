import { useContext, createContext } from "react";

const DisplayContext = createContext();
const useDisplayContext = () => useContext(DisplayContext);

const ImageDetailsContext = createContext();
const useImageDetailsContext = () => useContext(ImageDetailsContext);

export {
  DisplayContext,
  useDisplayContext,
  ImageDetailsContext,
  useImageDetailsContext,
};
