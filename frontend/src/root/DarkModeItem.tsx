/*
 * Copyright 2024 pyamsoft
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at:
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import React, { MouseEventHandler } from "react";
import { IconButton, useColorScheme } from "@mui/material";
import {
  Brightness6Outlined,
  DarkModeOutlined,
  LightModeOutlined,
} from "@mui/icons-material";

export const DarkModeItem: React.FunctionComponent = function () {
  const { mode, setMode } = useColorScheme();

  const handleToggleMode: MouseEventHandler = React.useCallback(
    ($event) => {
      $event.preventDefault();
      $event.stopPropagation();

      if (mode === "system") {
        setMode("light");
      } else if (mode === "light") {
        setMode("dark");
      } else if (mode === "dark") {
        setMode("system");
      }
    },
    [setMode, mode],
  );

  if (!mode) {
    return null;
  }

  return (
    <IconButton onClick={handleToggleMode}>
      {mode === "light" ? (
        <LightModeOutlined />
      ) : mode === "dark" ? (
        <DarkModeOutlined />
      ) : (
        <Brightness6Outlined />
      )}
    </IconButton>
  );
};
