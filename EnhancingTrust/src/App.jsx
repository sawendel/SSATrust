import {
  BrowserRouter,
  Routes,
  Route,
} from 'react-router-dom';
import ModeWrapper from './components/Common/ModeWrapper';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/workflow/:id" element={<ModeWrapper />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
