import { useState } from 'react';
import Paper from '@mui/material/Paper';
import InputBase from '@mui/material/InputBase';
import IconButton from '@mui/material/IconButton';
import SearchIcon from '@mui/icons-material/Search';
import LightMode from '@mui/icons-material/LightMode';
import DarkMode from '@mui/icons-material/DarkMode';
import './SearchBar.css';
import { FormControl, FormControlLabel, FormLabel, Grid, Radio, RadioGroup, Typography } from '@mui/material';

function SearchBar({ onSearch, theme }) {
  const [query, setQuery] = useState('');
  const [searchModel, setSearchModel] = useState('vsm');

  const handleSearch = (event) => {
    event.preventDefault();
    onSearch({ query, searchModel });
  };

  return (
    <Grid container spacing={2} alignItems="center">
      <Grid item>
        <Typography variant="h5">IR Service</Typography>
      </Grid>
      <Grid item xs>
        <Paper
          sx={{ p: '2px 4px', display: 'flex', alignItems: 'center' }}
        >
          <InputBase
            sx={{ flex: 1, ml: 1 }}
            placeholder="Enter text to search..."
            inputProps={{ 'aria-label': 'search' }}
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === 'Enter') {
                handleSearch(event);
              }
            }}
          />
          <IconButton type="button" sx={{ p: '10px' }} aria-label="search" onClick={handleSearch}>
            <SearchIcon />
          </IconButton>
        </Paper>
      </Grid>
      <Grid item>
        <IconButton type="button" sx={{ p: '10px' }} aria-label="search" onClick={theme.switchTheme}>
          {theme?.theme?.palette.mode === 'dark' ? <LightMode /> : <DarkMode />}
        </IconButton>
      </Grid>
      <Grid xs={12} item>
        <FormControl>
          <FormLabel id="search-model-label">Select search model:</FormLabel>
          <RadioGroup
            row
            aria-labelledby="search-model-label"
            name="search-model"
            value={searchModel}
            onChange={(event) => setSearchModel(event.target.value)}
          >
            <FormControlLabel value="vsm" control={<Radio />} label="Vector Space Model" />
            <FormControlLabel value="bm25" control={<Radio />} label="BM25" />
            <FormControlLabel value="qldps" control={<Radio />} label="Query LM" />
          </RadioGroup>
        </FormControl>
      </Grid>
    </Grid>
  );
}

export default SearchBar;