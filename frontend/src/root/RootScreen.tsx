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

import React from "react";
import { TopBar } from "./TopBar.tsx";
import { Stack } from "@mui/material";
import { Outlet } from "react-router-dom";

export const RootScreen: React.FunctionComponent = function () {
  return (
    <Stack direction="column" width="100%" overflow="hidden">
      <TopBar />
      <Stack direction="column" flexGrow={1} overflow="auto">
        <Outlet />
      </Stack>
    </Stack>
  );
};
