import { Grid, Paper, Typography } from "@mui/material";
import Highlighter from "react-highlight-words";

function DocumentViewer({ preview, queryTokens }) {

  const highlightKeywords = (text) => {
    return <Highlighter
      searchWords={queryTokens}
      autoEscape={true}
      textToHighlight={text}
    />
  }

  return (
    preview ? <Paper sx={{ m: 3 }}>
      <Grid sx={{ p: 4 }} container direction="column">
        <Grid item>
          <Typography variant="h4" sx={{ mb: 4 }}>Document Preview</Typography>
        </Grid>
        <Grid item container direction="row" justifyContent='space-between'>
          <Grid item>
            <Typography variant="body2" sx={{ mb: 2 }} >Document No. {preview.docno}</Typography>
          </Grid>
        </Grid>
        <Grid item>
          <Typography variant="h6" sx={{ mb: 2 }}>{highlightKeywords(preview.document.title)}</Typography>
        </Grid>
        <Grid item>
          <Typography variant="subtitle1" >{highlightKeywords(preview.document.author)}</Typography>
        </Grid>
        <Grid item>
          <Typography variant="subtitle2" sx={{ mb: 2 }} >{(highlightKeywords(preview.document.bib))}</Typography>
        </Grid>
        <Grid item>
          <Typography variant="body1" >{(highlightKeywords(preview.document.text))}</Typography>
        </Grid>
      </Grid>
    </Paper> : <></>
  );
}

export default DocumentViewer;