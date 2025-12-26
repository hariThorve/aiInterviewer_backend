// 1. will generate questions based on job titles recieved from the form data/user data.

// 2. used langchain with relative ai model to generate questions with respective answers.
import { ChatGroq } from "@langchain/groq";
import { HumanMessage, SystemMessage } from "@langchain/core/messages";
import { configDotenv } from "dotenv";
configDotenv()

// array of postions.
// this array is only for testing purpose. Originally the questions will be generated directly from the form data/user data.


// const jobs = [
//     "Physician",
//     "General Practitioner (GP)",
//     "Family Physician",
//     "Specialist Physician (various specialties)",
//     "Surgeon",
//     "Anesthesiologist",
//     "Psychiatrist",
//     "Pediatrician",
//     "Geriatrician",
//     "Cardiologist",
//     "Neurologist",
//     "Rheumatologist",
//     "Nephrologist",
//     "Oncologist",
//     "Dermatologist",
//     "Ophthalmologist",
//     "Otolaryngologist (ENT)",
//     "Urologist",
//     "Endocrinologist",
//     "Infectious Disease Specialist",
//     "Emergency Physician",
//     "Radiologist",
//     "Pathologist",
//     "Medical Geneticist",
//     "Physiatrist",
//     "Occupational Medicine Physician",
//     "Nurse Practitioner (NP)",
//     "Registered Nurse (RN)",
//     "Registered Psychiatric Nurse (RPN)",
//     "Licensed Practical Nurse (LPN)",
//     "Nurse Coordinator/Supervisor",
//     "Nursing Aide",
//     "Personal Support Worker (PSW)",
//     "Home Support Worker",
//     "Nurse Assistant",
//     "Physician Assistant",
//     "Midwife",
//     "Pharmacist",
//     "Pharmacy Technician",
//     "Pharmacy Assistant",
//     "Paramedic",
//     "Respiratory Therapist",
//     "Clinical Perfusionist",
//     "Cardiopulmonary Technologist",
//     "Physiotherapist",
//     "Occupational Therapist",
//     "Speech-Language Pathologist",
//     "Audiologist",
//     "Dietitian/Nutritionist",
//     "Social Worker",
//     "Psychologist",
//     "Psychotherapist",
//     "Mental Health Counselor",
//     "Addiction Counselor",
//     "Behavioral Therapist",
//     "Developmental Service Worker",
//     "Special Education Teacher",
//     "Kinesiologist",
//     "Massage Therapist",
//     "Chiropractor",
//     "Dental Hygienist",
//     "Dental Therapist",
//     "Dentist",
//     "Dental Assistant",
//     "Optometrist",
//     "Medical Laboratory Technologist",
//     "Medical Laboratory Technician",
//     "Medical Sonographer",
//     "Medical Radiation Technologist",
//     "Cardiology Technologist",
//     "Medical Imaging Technologist",
//     "Medical Office Assistant",
//     "Clinic Administrator",
//     "Health Information Manager",
//     "Rehabilitation Assistant",
//     "Recreation Therapist",
//     "Traditional Chinese Medicine Practitioner",
//     "Acupuncturist",
//     "Naturopathic Doctor",
//     "Homeopath",
//     "Ayurvedic Practitioner",
//     "Yoga Therapist",
//     "Podiatrist/Foot Care Nurse",
//     "Wound Care Nurse/Specialist",
//     "Immunizer/Vaccinator"
// ];


const generateAiQuestions = async (JobTitle) => {
    const systemPrompt = "You are a helpful assistant, you will recieve a job title and you have to generate questions and their respective answers based on that job title which can be asked in an interview. Remeber the json format of the response, [{question: '', answer: ''}]. Make sure generate 10 questions and answers respectively. No extra words only array of objects."
    
    const prompt = "Generate questions and answers for the job title: " + JobTitle
    
    
    const model = new ChatGroq({
        apiKey: process.env.GROQ_API_KEY, // API key from environment variables
        model: "llama-3.3-70b-versatile", // Using Llama 3.3 70B
        temperature: 0, // Low temperature for consistent, deterministic results
    });
    const messages = [
        new SystemMessage(systemPrompt), // System prompt with evaluation criteria
        new HumanMessage(prompt), // User prompt with transcript
    ];
    
    const result = await model.invoke(messages);
    console.log(result.content); // Log results for debugging
    return result.content; // Return the evaluation results
    
}

// generateAiQuestions("Health Information Manager")

export default generateAiQuestions;


