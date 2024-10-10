/*
  The MIT License

  Copyright (c) 2017-2019 EclipseSource Munich
  https://github.com/eclipsesource/jsonforms

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.
*/
import React from "react";

import ErrorOutlineIcon from "@mui/icons-material/ErrorOutline";
import { Badge, Tooltip, styled } from "@mui/material";

const StyledBadge = styled(Badge)(({ theme }: any) => ({
  color: theme.palette.error.main,
}));

export interface ValidationProps {
  errorMessages: string;
  id: string;
}

const ValidationIcon: React.FC<ValidationProps> = ({ errorMessages, id }) => {
  return (
    <Tooltip id={id} title={errorMessages}>
      <StyledBadge badgeContent={errorMessages.split("\n").length}>
        <ErrorOutlineIcon color="inherit" />
      </StyledBadge>
    </Tooltip>
  );
};

export default ValidationIcon;
