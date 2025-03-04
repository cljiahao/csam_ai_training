import { createContext, useContext } from "react";

const SettingsFinderContext = createContext(null);

export const useSettingsFinderContext = () => useContext(SettingsFinderContext);

export default SettingsFinderContext;
