import { useState, useEffect, useMemo } from 'react';
import { Container, Row, Col, Button } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router-dom';
import { ModeResults, ModeTypes, Modes, Events, QueryParams } from '../../constants';
import { useQuery } from '../../hooks';
import steps from '../../config/steps.json';
import Email from '../Common/Email';
import Audio from '../Common/AudioPlayer';
import Letter from '../Common/Letter';
import Sms from '../Common/Sms';
import Webpage from '../Common/Webpage';
import screenfull from 'screenfull';
import { logger } from '../../services';

const ModeWrapper = () => {
  const { id } = useParams();
  const query = useQuery();
  const navigate = useNavigate();
  const workflow = useMemo(() => steps.workflows.find((x) => x.id === id), [id]);
  const workflowSteps = useMemo(() => workflow?.steps, [workflow]);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [stepIndex, setStepIndex] = useState(0);
  const [selected, setSelected] = useState();
  const [clicked, setClicked] = useState(false);
  const [displayTooltips, setDisplayTooltips] = useState(false);
  const currentStep = workflowSteps[stepIndex];
  const isLastStep = stepIndex === workflowSteps?.length - 1;
  const isFirstStep = stepIndex === 0;
  const isEducational = workflow.mode === Modes.EDUCATIONAL;

  useEffect(() => {
    function onScreenChange() {
      setIsFullscreen(screenfull.isFullscreen);
    };
    try {
      screenfull.on('change', onScreenChange);
      if (query.get(QueryParams.FULLSCREEN) !== 'false') {
        if (screenfull.isEnabled) {
          screenfull.request();
        }
        return () => {
          screenfull.off('change', onScreenChange);
          screenfull.exit().then();
        }
      }
    } catch (e) {
      console.error(e);
    }
  }, []);

  const logEvent = (event, metadata) => {
    return logger.logEvent(query.get(QueryParams.UID), id, event, currentStep.template, currentStep.type, metadata);
  };

  const stepElement = useMemo(() => {
    switch (currentStep.type) {
      case ModeTypes.EMAIL:
        return <Email logEvent={logEvent} type={currentStep.type} showTooltips={displayTooltips} templateUrl={`/emails/${currentStep.template}`} />;
      case ModeTypes.SMS:
        return <Sms logEvent={logEvent} type={currentStep.type} showTooltips={displayTooltips} templateUrl={`/sms/${currentStep.template}`} />;
      case ModeTypes.LETTER:
        return <Letter logEvent={logEvent} type={currentStep.type} showTooltips={displayTooltips} templateUrl={`/letters/${currentStep.template}`} />;
      case ModeTypes.AUDIO:
        return <Audio logEvent={logEvent} type={currentStep.type} audioScr={`/audios/${currentStep.template}`} tooltip={currentStep.tooltip} showTooltips={displayTooltips} />;
      case ModeTypes.WEBPAGE:
          return <Webpage
            logEvent={logEvent}
            type={currentStep.type}
            showTooltips={displayTooltips}
            mobileTemplate={currentStep.mobileTemplate && `/webpages/${currentStep.mobileTemplate}`}
            templateUrl={`/webpages/${currentStep.template}`}
          />;
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

  const getNextButtonText = () => {
    if (displayTooltips) {
      return 'Next';
    }
    if (!selected) {
      return 'Skip';
    }
    return 'Send';
  }

  const redirect = () => {
    const redirect = query.get(QueryParams.REDIRECT_URL);
    const userId = query.get(QueryParams.UID);  // SW: include this in the URL string if needed
    if (redirect) {
      window.location.href = redirect;
    } else {
      navigate('/', { replace: true });
    }
  };

  const onNext = () => {
    setClicked(true);
    if (!displayTooltips && !selected) {
       logEvent(Events.PAGE_SKIPPED);

      if (isLastStep) {
        logEvent(Events.PAGE_SKIPPED).then((_) => {
          setClicked(false);
          redirect();
          return;
        });
      }
      setClicked(false);
      setStepIndex(stepIndex + 1);
      return;
    }

    if (!isEducational || !displayTooltips) {
      if (!isLastStep) {
        logEvent(selected === ModeResults.REAL ? Events.MARKED_REAL : Events.MARKED_SCAM);
        setClicked(false);
      } else {
        logEvent(selected === ModeResults.REAL ? Events.MARKED_REAL : Events.MARKED_SCAM).then((_) => {
          setClicked(false);
          redirect();
          return;
        });
      }
    }

    if (isEducational && !displayTooltips) {
      setDisplayTooltips(true);
      setClicked(false);
      return;
    }

    if (!isLastStep) {
      setSelected(undefined);
      setClicked(false);
      setStepIndex(stepIndex + 1);
      setDisplayTooltips(false);
      window.scrollTo(0, 0);
      return;
    }

  };

  const getDisplayText = () => {
    if (displayTooltips) {
      return <>Thank you. This communication was {currentStep.result}. Please see below for why</>;
    } else if (isFirstStep) {
      return <>Is the following <strong>{currentStep.type}</strong> {ModeResults.REAL} or a {ModeResults.SCAM}?</>;
    } else {
      return <>Thank you. Now, is this <strong>{currentStep.type}</strong> {ModeResults.REAL} or a {ModeResults.SCAM}?</>;
    }
  };
 
  return (
    <>
      <Container fluid className={`et-mode-wrapper ${displayTooltips ? 'bg-prussian' : 'bg-black'}`}>
        <Row className="align-items-center">
          <Col>
            <Row className="align-items-center">
              <Col lg="auto" md={12}>
                <h5 className="et-mode-wrapper__qn me-4 my-lg-0 my-3 py-4">{getDisplayText()}</h5> 
              </Col>
              {!displayTooltips && (
                <Col>
                  <Row className="mb-lg-0 mb-3">
                    <Col xs={6} lg="auto">
                      <Button
                        className="w-100 w-lg-auto et-mode-wrapper__result-btn et-mode-wrapper__result-btn-success px-4 me-4"
                        variant="outline-success"
                        active={ModeResults.REAL === selected}
                        onClick={(e) => onResultClick(e, ModeResults.REAL)}
                      >
                        {ModeResults.REAL}
                        <i className="et-check" />
                      </Button>
                    </Col>
                    <Col xs={6} lg="auto">
                      <Button
                        className="w-100 w-lg-auto et-mode-wrapper__result-btn et-mode-wrapper__result-btn-danger px-4"
                        variant="outline-danger"
                        active={ModeResults.SCAM === selected}
                        onClick={(e) => onResultClick(e, ModeResults.SCAM)}
                      >
                        {ModeResults.SCAM}
                        <i className="et-close" />
                      </Button>
                    </Col>
                  </Row>
                </Col>
              )}
            </Row>
          </Col>
          {isFullscreen && (
            <Col lg="auto" md="12" className="">
              <Button
                className="et-mode-wrapper__exit-full mb-3 mb-lg-0 w-100"
                variant="outline-white"
                onClick={() => screenfull.exit().then()}
              >
                Exit full-screen mode
              </Button>
            </Col>
          )}
		  {  (displayTooltips || selected) && (  
          <Col lg="auto" md="12" className="p-0">
            <Button
              variant="secondary"
              className="px-xsl-5 px-lg-2 py-4 rounded-0 w-100"
              onClick={onNext}
              disabled={clicked}
            >
              <span className="pe-2 pb-1">{getNextButtonText()}</span>
              <i className="et-caret-right" />
            </Button>
          </Col>
          )}
        </Row>
      </Container>
      {stepElement}
    </>
  );
};

export default ModeWrapper;
