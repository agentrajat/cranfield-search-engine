import { Grid } from "@mui/material";
import Home from "./Home";
import DocumentViewer from "./DocumentViewer";
import { useState } from "react";
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

const lightTheme = createTheme({
  palette: {
    mode: 'light',
  },
});

function App() {

  const [preview, setPreview] = useState(null);
  const [queryTokens, setQueryTokens] = useState([]);
  const [theme, setTheme] = useState(darkTheme);

  const switchTheme = () => {
    if (theme.palette.mode === 'dark') {
      setTheme(lightTheme);
    } else {
      setTheme(darkTheme);
    }
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Grid container direction="row">
        <Grid item xs>
          <Home setPreview={setPreview} setQueryTokens={setQueryTokens} theme={{theme, switchTheme}} />
        </Grid>
        <Grid item xs>
          <DocumentViewer preview={preview} queryTokens={queryTokens} />
        </Grid>
      </Grid>
    </ThemeProvider>
  );
}

export default App;