import { Chip, Grid, Link, Typography } from "@mui/material";

function Result({ result, setPreview }) {
  return (
    <Grid container justifyContent='space-between'>
      <Grid item xs={12}>
        <Link underline="hover" sx={{cursor: 'pointer'}} onClick={() => setPreview(result)}>
          {result.document?.title}
        </Link>
      </Grid>
      <Grid item>
        <Typography variant="body2">{`Rank: ${result.rank}`}</Typography>
      </Grid>
      <Grid item>
        <Typography variant="body2">{`Document No.: ${result.docno}`}</Typography>
      </Grid>
    </Grid>
  );
}

export default Result;