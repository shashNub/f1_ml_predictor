import React, {useState} from "react";
import GlobalStyles from './styles/GlobalStyles';
import PredictorPanel from './components/PredictorPanel';
import LoadingScreen from './components/LoadingScreen';
import ResultDisplay from './components/ResultDisplay';
import './App.css';

function App() {
  const [prixName, setPrixName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [predictions, setPredictions] = useState([]);
  const [error, setError] = useState('');


  return(
    <>
      <GlobalStyles />
      <PredictorPanel 
        prixName = {prixName}
        setPrixName = {setPrixName}
        setPredictions = {setPredictions}
        setIsLoading = {setIsLoading}
        setError ={setError}

      />
      {error && (<p style={{ color: 'red', textAlign: 'center', marginTop: '1rem' }}>{error}</p>)}
      {isLoading && <LoadingScreen />}
      <ResultDisplay predictions={predictions} error={error} />
    </>
  );
}

export default App;
