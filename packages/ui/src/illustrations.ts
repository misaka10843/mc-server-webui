import art0 from './assets/illustrations/mascot-auth-welcome.webp'
import art1 from './assets/illustrations/state-not-found.webp'
import art2 from './assets/illustrations/state-no-applications.webp'
import art3 from './assets/illustrations/state-no-results.webp'
import art4 from './assets/illustrations/state-service-unavailable.webp'
import art5 from './assets/illustrations/mascot-developer-welcome.webp'
import art6 from './assets/illustrations/state-access-restricted.webp'
import art7 from './assets/illustrations/state-session-expired.webp'
import art8 from './assets/illustrations/state-no-records.webp'
import art9 from './assets/illustrations/state-complete.webp'
import art10 from './assets/illustrations/mascot-guide-helper.webp'
import art11 from './assets/illustrations/mascot-face-neutral.webp'

export const illustrations = {
  'auth-welcome': { src: art0, width: 880, height: 1100 },
  'not-found': { src: art1, width: 480, height: 480 },
  'no-applications': { src: art2, width: 480, height: 480 },
  'no-results': { src: art3, width: 480, height: 480 },
  'service-unavailable': { src: art4, width: 480, height: 480 },
  'developer-welcome': { src: art5, width: 900, height: 675 },
  'access-restricted': { src: art6, width: 480, height: 480 },
  'session-expired': { src: art7, width: 480, height: 480 },
  'no-records': { src: art8, width: 480, height: 480 },
  'complete': { src: art9, width: 480, height: 480 },
  'guide-helper': { src: art10, width: 480, height: 480 },
  'face-neutral': { src: art11, width: 192, height: 192 },
} as const

export type MoeIllustrationName = keyof typeof illustrations
