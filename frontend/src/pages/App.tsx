import { Route, Routes } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';

import { BaseLayout } from '../layouts/BaseLayout';
import { DashboardPage } from './DashboardPage';
import { AutomationPage } from './AutomationPage';
import { HotspotPage } from './HotspotPage';
import { SecurityPage } from './SecurityPage';

const App = () => {
  return (
    <BaseLayout>
      <AnimatePresence mode="wait">
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/automation" element={<AutomationPage />} />
          <Route path="/hotspot" element={<HotspotPage />} />
          <Route path="/security" element={<SecurityPage />} />
        </Routes>
      </AnimatePresence>
    </BaseLayout>
  );
};

export default App;
