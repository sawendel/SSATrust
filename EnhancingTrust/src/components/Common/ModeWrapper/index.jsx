import { useState, useMemo } from 'react';
import { Container, Row, Col, Button } from 'react-bootstrap';
import { useParams } from 'react-router-dom';
import { ModeResults, ModeTypes, Modes } from '../../../constants';
import steps from '../../../config/steps.json';
import Email from '../Email';
import Audio from '../AudioPlayer';
import Letter from '../Letter';
import Sms from '../Sms';

const ModeWrapper = () => {
  const { id } = useParams();
  const workflow = useMemo(() => steps.workflows.find((x) => x.id === id), [id]);
  const workflowSteps = useMemo(() => workflow?.steps, [workflow]);
  const [stepIndex, setStepIndex] = useState(0);
  const [selected, setSelected] = useState();
  const [displayTooltips, setDisplayTooltips] = useState(false);
  const currentStep = workflowSteps[stepIndex];
  const isLastStep = stepIndex === workflowSteps?.length - 1;
  const isEducational = workflow.mode === Modes.EDUCATIONAL;

  const stepElement = useMemo(() => {
    switch (currentStep.type) {
      case ModeTypes.EMAIL:
        return <Email showTooltips={displayTooltips} templateUrl={`/emails/${currentStep.template}`} />;
      case ModeTypes.SMS:
        return <Sms showTooltips={displayTooltips} templateUrl={`/sms/${currentStep.template}`} />;
      case ModeTypes.LETTER:
        return <Letter showTooltips={displayTooltips} templateUrl={`/letters/${currentStep.template}`} />;
      case ModeTypes.AUDIO:
        return <Audio audioScr={`/audios/${currentStep.template}`} />;
      default:
        throw new Error('Template not recognized');
    }
  }, [stepIndex, workflowSteps, displayTooltips]);

  const onResultClick = (e, result) => {
    if (selected === result) {
      setSelected(null);
    } else {
      setSelected(result);
    }
    e.currentTarget.blur();
  }

  const onNext = () => {
    if (isEducational && !displayTooltips) {
      setDisplayTooltips(true);
      return;
    }

    if (!isLastStep) {
      setSelected(undefined);
      setStepIndex(stepIndex + 1);
      setDisplayTooltips(false);
    }
  };
 
  return (
    <>
      <Container fluid className="et-mode-wrapper bg-info">
        <Row className="align-items-center">
          <Col>
            <Row className="align-items-center">
              <Col md="auto" sm={12}>
                <p className="et-mode-wrapper__qn me-4 my-md-0 my-3">Is the following <strong>{currentStep.type}</strong> {ModeResults.REAL} or {ModeResults.FAKE}?</p>
              </Col>
              {!displayTooltips && (
                <Col>
                  <Row className="mb-md-0 mb-3">
                    <Col xs={6} md="auto">
                      <Button
                        className="w-100 w-md-auto et-mode-wrapper__result-btn et-mode-wrapper__result-btn-success px-4 me-4"
                        variant="outline-white"
                        active={ModeResults.REAL === selected}
                        onClick={(e) => onResultClick(e, ModeResults.REAL)}
                      >
                        {ModeResults.REAL}
                        <i className="et-check" />
                      </Button>
                    </Col>
                    <Col xs={6} md="auto">
                      <Button
                        className="w-100 w-md-auto et-mode-wrapper__result-btn et-mode-wrapper__result-btn-danger px-4"
                        variant="outline-white"
                        active={ModeResults.FAKE === selected}
                        onClick={(e) => onResultClick(e, ModeResults.FAKE)}
                      >
                        {ModeResults.FAKE}
                        <i className="et-close" />
                      </Button>
                    </Col>
                  </Row>
                </Col>
              )}
            </Row>
          </Col>
          <Col md="auto" sm="12" className="p-0">
            <Button
              variant="secondary"
              className={`${!selected ? 'invisible d-md-block d-none' : ''} px-5 py-3 rounded-0 w-100`}
              onClick={onNext}
            >
              <span className="pe-2 pb-1">{isLastStep ? 'Complete' : 'Next'}</span>
              <i className="et-caret-right" />
            </Button>
          </Col>
        </Row>
      </Container>
      {stepElement}
    </>
  );
};

export default ModeWrapper;
