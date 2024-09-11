import { Box, Grid, Pagination, Typography } from '@mui/material';
import SearchBar from '../components/SearchBar/SearchBar';
import Result from '../components/Result/Result';
import { fetchDocumentsAPI, initializeAPI, invokeSearchAPI } from '../services/APIService';
import { useState, useEffect } from 'react';

const PAGE_SIZE = 10;
const DEFAULT_PAGE = 1;

function Home({ setPreview, setQueryTokens, theme }) {

  const [searchResults, setSearchResults] = useState([]);
  const [page, setPage] = useState(DEFAULT_PAGE);
  const [noResults, setNoResults] = useState(false);

  useEffect(() => {
    initializeAPI();
    return () => { };
  }, []);

  const invokeSearch = ({ query, searchModel }) => {
    if (query && query.length > 0) {
      invokeSearchAPI({ query, searchModel }).then((data) => {
        setPreview(null);
        if (data?.results?.length === 0) {
          setNoResults(true);
          setSearchResults([]);
          setQueryTokens([])
          return;
        } else {
          setNoResults(false);
          const searchData = data.results.map((elem, index) => {
            return { ...elem, rank: index + 1 };
          });
          setQueryTokens(data.tokens);
          loadPage(DEFAULT_PAGE, searchData);
        }
      });
    }
  };

  const loadPage = (newPage, searchData) => {
    setPage(newPage);
    const pageStart = (newPage - 1) * PAGE_SIZE;
    const pageEnd = pageStart + PAGE_SIZE;

    let fetchingList = [];
    for (let i = pageStart; i < pageEnd; i++) {
      if (i < searchData.length && !searchData[i].document) {
        fetchingList.push(searchData[i].docno);
      }
    }

    if (fetchingList.length > 0) {
      fetchDocumentsAPI(fetchingList).then((data) => {
        if (data && data.length > 0) {
          const updatedResults = [...searchData];
          for (let i = 0; i < data.length; i++) {
            const docno = data[i].docno;
            const index = fetchingList.indexOf(docno);
            if (index > -1) {
              updatedResults[pageStart + index].document = data[i];
            }
          }
          setSearchResults(updatedResults);
        }
      });
    }
  }

  const getPageSize = () => {
    console.log(searchResults.length)
    return Math.ceil(searchResults.length / PAGE_SIZE);
  }

  const handlePageChange = (event, value) => {
    loadPage(value, searchResults);
  }

  const getCurrentPage = () => {
    const pageStart = (page - 1) * PAGE_SIZE;
    const pageEnd = pageStart + PAGE_SIZE;
    return searchResults.slice(pageStart, pageEnd);
  }

  return (
    <Box sx={{ padding: 3 }}>
      <Box component="header">
        <SearchBar onSearch={invokeSearch} theme={theme} />
      </Box>
      <Box component="section" sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        {searchResults?.length > 0 && (<>
          <Typography variant="h6" sx={{ mb: 3, mt: 2, alignSelf: 'flex-start' }}>Search Results (About {searchResults.length} records found)</Typography>
          <Grid container spacing={4} direction="column">
            {getCurrentPage().map((result, index) => (
              result.document ? (
                <Grid key={index} item>
                  <Result result={result} setPreview={setPreview} />
                </Grid>
              ) : <></>
            ))}
          </Grid>
          <Pagination sx={{ mt: 3 }} count={getPageSize()} defaultPage={1} page={page} onChange={handlePageChange} />
        </>)}
        {noResults && (
          <Typography variant="h6" sx={{ mb: 3 }}>No results found</Typography>
        )}
      </Box>
    </Box>
  );
}

export default Home;
