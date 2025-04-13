using UnityEngine;

public class AvatarAnimationController : MonoBehaviour
{
    public Animator avatarAnimator;

    private void ResetAllTriggers()
    {
        avatarAnimator.ResetTrigger("SomeInfo");
        avatarAnimator.ResetTrigger("IwantMore");
        avatarAnimator.ResetTrigger("Bye");
        avatarAnimator.ResetTrigger("Hey");
    }

    public void PlayHappyIdle()
    {
        ResetAllTriggers();
        avatarAnimator.SetTrigger("SomeInfo");
    }

    public void PlayExcited()
    {
        ResetAllTriggers();
        avatarAnimator.SetTrigger("IwantMore");
    }

    public void Bye()
    {
        ResetAllTriggers();
        avatarAnimator.SetTrigger("Bye");
    }    

    public void Hey()
    {
        ResetAllTriggers();
        avatarAnimator.SetTrigger("Hey");
    }
}
