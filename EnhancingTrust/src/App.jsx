import {
  BrowserRouter,
  Routes,
  Route,
} from 'react-router-dom';
import HomePage from './components/HomePage';
import ModeWrapper from './components/Common/ModeWrapper';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" index exact element={<HomePage id={1} />} />
        <Route path="/workflow/:id" element={<ModeWrapper />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
